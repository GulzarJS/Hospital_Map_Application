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
	_ "strconv"
	"sync"
	"time"

	_ "fyne.io/fyne/widget"
	"github.com/paulmach/osm/osmpbf"

	_ "image/color"

	"github.com/paulmach/osm"

	_ "fyne.io/fyne"
	_ "fyne.io/fyne/app"
	_ "fyne.io/fyne/canvas"
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
		{"a_node_id", "b_node_id", "distance", "a_node_lat", "a_node_lon", "b_node_lat", "b_node_lon"},
	}

	nodesHospitals := [][]string{
		{"node_id", "name", "lat", "lon"},
	}

	startInit := time.Now()

	var mu sync.Mutex

	boundsBaku := bounds{
		topLat:    40.3829,
		bottomLat: 40.3691,
		leftLon:   49.8291,
		rightLon:  49.8596,
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

			if boundsBaku.checkBounds(*node, *node) {
				if name, ok := node.TagMap()["amenity"]; ok && name == "hospital" {
					//log.Printf("amenity: %v", node.TagMap())
					hospitalName := ""
					if name, ok := node.TagMap()["name:tr"]; ok {
						hospitalName = name
					}
					if name, ok := node.TagMap()["name:az"]; ok {
						hospitalName = name
					}
					if name, ok := node.TagMap()["name:en"]; ok {
						hospitalName = name
					}
					if name, ok := node.TagMap()["name"]; ok {
						hospitalName = name
					}

					nodesHospitals = append(nodesHospitals, []string{
						fmt.Sprintf("%d", int64(node.ID)),
						hospitalName,
						fmt.Sprintf("%f", node.Lat),
						fmt.Sprintf("%f", node.Lon),
					})
				}
			}

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
									fmt.Sprintf("%f", firstNode.Lat),
									fmt.Sprintf("%f", firstNode.Lon),
									fmt.Sprintf("%f", Nodes[nodeID].Lat),
									fmt.Sprintf("%f", Nodes[nodeID].Lon),
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

	ElemSizeVerbose("records", records)

	startInit = time.Now()

	fCsv, err := os.Create(".\\data\\datas.csv")

	defer fCsv.Close()

	if err != nil {
		panic(err)
	}

	w := csv.NewWriter(fCsv)

	fCsvHospitals, err := os.Create(".\\data\\datasHospitals.csv")

	defer fCsvHospitals.Close()

	if err != nil {
		panic(err)
	}

	wHospitals := csv.NewWriter(fCsvHospitals)

	elapsed = time.Since(startInit)
	log.Printf("CSV initialization took %s", elapsed)

	startWrite := time.Now()

	err = w.WriteAll(records)

	if err != nil {
		panic(err)
	}

	err = wHospitals.WriteAll(nodesHospitals)

	if err != nil {
		panic(err)
	}

	elapsed = time.Since(startWrite)
	log.Printf("CSV write took %s", elapsed)

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

func ElemSizeVerbose(name string, container interface{}) {
	b := new(bytes.Buffer)
	if err := gob.NewEncoder(b).Encode(container); err != nil {
		fmt.Println("Error reading size")
		return
	}

	fmt.Printf("Size of %s is %d\n", name, b.Len())
}
