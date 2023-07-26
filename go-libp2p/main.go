package main

import (
	"context"
	"fmt"
	"github.com/libp2p/go-libp2p"
	dht "github.com/libp2p/go-libp2p-kad-dht"
	"github.com/libp2p/go-libp2p/core/host"
	peerstore "github.com/libp2p/go-libp2p/core/peer"
	"github.com/libp2p/go-libp2p/core/routing"
	"github.com/libp2p/go-libp2p/p2p/protocol/ping"
	"github.com/multiformats/go-multiaddr"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	// The context governs the lifetime of the libp2p node.
	// Cancelling it will stop the the host.
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	var idht *dht.IpfsDHT
	var err error
	InitTracing()
	// start a libp2p node with default settings
	node, err := libp2p.New(libp2p.ListenAddrStrings("/ip4/127.0.0.1/tcp/0"),
		libp2p.Ping(false),
		libp2p.Routing(func(h host.Host) (routing.PeerRouting, error) {
			idht, err = dht.New(ctx, h)
			return idht, err
		}))
	if err != nil {
		panic(err)
	}

	// The last step to get fully up and running would be to connect to
	// bootstrap peers (or any other peers). We leave this commented as
	// this is an example and the peer will die as soon as it finishes, so
	// it is unnecessary to put strain on the network.

	/*
		// This connects to public bootstrappers
		for _, addr := range dht.DefaultBootstrapPeers {
			pi, _ := peer.AddrInfoFromP2pAddr(addr)
			// We ignore errors as some bootstrap peers may be down
			// and that is fine.
			h2.Connect(ctx, *pi)
		}
	*/

	// configure our own ping protocol
	pingService := &ping.PingService{Host: node}
	node.SetStreamHandler(ping.ID, pingService.PingHandler)

	// print the node's listening addresses
	fmt.Println("Listen addresses:", node.Addrs())

	// print the node's PeerInfo in multiaddr format
	peerInfo := peerstore.AddrInfo{
		ID:    node.ID(),
		Addrs: node.Addrs(),
	}
	addrs, err := peerstore.AddrInfoToP2pAddrs(&peerInfo)
	fmt.Println("libp2p node address:", addrs[0])

	// if a remote peer has been passed on the command line, connect to it
	// and send it 5 ping messages, otherwise wait for a signal to stop
	if len(os.Args) > 1 {
		addr, err := multiaddr.NewMultiaddr(os.Args[1])
		if err != nil {
			panic(err)
		}
		peer, err := peerstore.AddrInfoFromP2pAddr(addr)
		if err != nil {
			panic(err)
		}
		if err := node.Connect(context.Background(), *peer); err != nil {
			fmt.Println(err)
			panic(err)
		}
		fmt.Println("sending 5 ping messages to", addr)
		ch := pingService.Ping(context.Background(), peer.ID)
		for i := 0; i < 5; i++ {
			res := <-ch
			fmt.Println("got ping response!", "RTT:", res.RTT)
		}
	} else {
		// wait for a SIGINT or SIGTERM signal
		ch := make(chan os.Signal, 1)
		signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
		<-ch
		fmt.Println("Received signal, shutting down...")
	}
	// shut the node down
	if err := node.Close(); err != nil {
		panic(err)
	}
}
