package main

import (
	"bytes"
	"context"
	"encoding/csv"
	"encoding/gob"
	"fmt"
	"log"
	"math"
	"os"
	"sync"
	"time"

	"github.com/paulmach/osm/osmpbf"

	"github.com/paulmach/osm"
)

var Nodes map[osm.NodeID]osm.Node
var Ways map[osm.WayID]osm.Way

type bounds struct {
	topLat    float64
	bottomLat float64
	leftLon   float64
	rightLon  float64
}

func main() {

	startMain := time.Now()

	Nodes = make(map[osm.NodeID]osm.Node)
	Ways = make(map[osm.WayID]osm.Way)

	records := [][]string{
		{"a_node_id", "b_node_id", "distance"},
	}

	startInit := time.Now()

	var mu sync.Mutex

	boundsBaku := bounds{
		topLat:    40.4670,
		bottomLat: 40.3328,
		leftLon:   49.7487,
		rightLon:  49.9624,
	}

	f, err := os.Open(".\\data\\azerbaijan-latest.osm.pbf")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	scanner := osmpbf.New(context.Background(), f, 8)
	defer scanner.Close()

	elapsed := time.Since(startInit)
	log.Printf("Main initialization took %s", elapsed)

	startScan := time.Now()

	for scanner.Scan() {
		o := scanner.Object()

		switch o.ObjectID().Type() {
		case "node":
			var node *osm.Node = o.(*osm.Node)
			Nodes[node.ID] = *node

			break
		case "way":
			var way *osm.Way = o.(*osm.Way)
			Ways[way.ID] = *way

			if _, ok := way.TagMap()["highway"]; ok {
				firstFlag := true
				var firstNode osm.Node
				for _, nodeID := range way.Nodes.NodeIDs() {
					if firstFlag {
						firstFlag = false
						firstNode = Nodes[nodeID]
					} else {

						if boundsBaku.checkBounds(firstNode, Nodes[nodeID]) {
							mu.Lock()
							records = append(records,
								[]string{
									fmt.Sprintf("%d", int64(firstNode.ID)),
									fmt.Sprintf("%d", int64(Nodes[nodeID].ID)),
									fmt.Sprintf("%f", calcDist(firstNode, Nodes[nodeID])),
								})

							mu.Unlock()
						}

						firstNode = Nodes[nodeID]

					}
				}
			}

		}
	}

	elapsed = time.Since(startScan)
	log.Printf("Scanning took %s", elapsed)

	elemSizeVerbose("records", records)

	startInit = time.Now()

	fCsv, err := os.Create(".\\data\\datas.csv")

	defer fCsv.Close()

	if err != nil {
		panic(err)
	}

	w := csv.NewWriter(fCsv)

	elapsed = time.Since(startInit)
	log.Printf("CSV initialization took %s", elapsed)

	startWrite := time.Now()

	err = w.WriteAll(records)

	elapsed = time.Since(startWrite)
	log.Printf("CSV write took %s", elapsed)

	if err != nil {
		panic(err)
	}

	elapsed = time.Since(startMain)
	log.Printf("Program took %s", elapsed)
}

func calcLon(lon float64) float64 {
	return (lon - 49.8533300) * 200000
}

func calcLat(lat float64) float64 {
	return (lat - 40.3752500) * 200000
}

func calcDist(aNode, bNode osm.Node) float64 {
	return math.Sqrt(math.Pow(float64(aNode.Lat)-float64(bNode.Lat), 2) + math.Pow(float64(aNode.Lon)-float64(bNode.Lon), 2))
}

func (boundsA bounds) checkBounds(aNode, bNode osm.Node) bool {
	return aNode.Lat <= boundsA.topLat && aNode.Lat >= boundsA.bottomLat &&
		aNode.Lon >= boundsA.leftLon && aNode.Lon <= boundsA.rightLon &&
		bNode.Lat <= boundsA.topLat && bNode.Lat >= boundsA.bottomLat &&
		bNode.Lon >= boundsA.leftLon && bNode.Lon <= boundsA.rightLon
}

func elemSizeVerbose(name string, container interface{}) {
	b := new(bytes.Buffer)
	if err := gob.NewEncoder(b).Encode(container); err != nil {
		fmt.Println("Error reading size")
		return
	}

	fmt.Printf("Size of %s is %f\n", name, float64(b.Len())/1024)
}
