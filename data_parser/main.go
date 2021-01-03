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
	"strconv"
	_ "strconv"
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

	// Keep ways and nodes in a map for later access
	Nodes = make(map[osm.NodeID]osm.Node)
	Ways = make(map[osm.WayID]osm.Way)

	// csv file array with headers
	records := [][]string{
		{"a_node_id", "b_node_id", "distance", "a_node_lat", "a_node_lon", "b_node_lat", "b_node_lon"},
	}

	nodesHospitals := [][]string{
		{"node_id", "name", "lat", "lon", "nearestWayNode"},
	}

	startInit := time.Now()

	// Take this section of map
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

	// Loop through objects in map file
	for scanner.Scan() {
		o := scanner.Object()

		switch o.ObjectID().Type() {
		case "node":
			var node *osm.Node = o.(*osm.Node)
			Nodes[node.ID] = *node

			// check if the node is inside the section's bounds
			if boundsBaku.checkBounds(*node, *node) {

				// check if the node is a hospital
				if name, ok := node.TagMap()["amenity"]; ok && name == "hospital" {

					// get hospital's name
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

					// add it to the csv array
					nodesHospitals = append(nodesHospitals, []string{
						fmt.Sprintf("%d", int64(node.ID)),
						hospitalName,
						fmt.Sprintf("%f", node.Lat),
						fmt.Sprintf("%f", node.Lon),
						"0",
					})
				}
			}

			break
		case "way":
			var way *osm.Way = o.(*osm.Way)
			Ways[way.ID] = *way

			// check if the way is a road
			// Since osm file assumes every line in the map as a way, we need to only get the roads
			if _, ok := way.TagMap()["highway"]; ok {
				firstFlag := true
				var firstNode osm.Node
				for _, nodeID := range way.Nodes.NodeIDs() {

					// needed to build ways with two nodes
					if firstFlag {
						firstFlag = false
						firstNode = Nodes[nodeID]
					} else {

						// check if the way's nodes are inside the section's bounds
						if boundsBaku.checkBounds(firstNode, Nodes[nodeID]) {

							// add the way to csv array
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

							// this part finds the nearest way node to the hospital
							// since all nodes come before ways in osm files,
							// we can safely assume that all way nodes are already in our
							// Nodes array
							for i, nodeHospital := range nodesHospitals {
								if nodeHospital[4] == "0" {
									nodesHospitals[i][4] = fmt.Sprintf("%d", firstNode.ID)
								} else {
									hospitalNodeID, _ := strconv.Atoi(nodeHospital[0])
									hospitalNearestNodeID, _ := strconv.Atoi(nodeHospital[4])

									nearestDistance := calcDist(Nodes[osm.NodeID(hospitalNodeID)], Nodes[osm.NodeID(hospitalNearestNodeID)])

									// check if any of the nodes in the way are near to the hospital's node
									if nearestDistance > calcDist(Nodes[osm.NodeID(hospitalNodeID)], firstNode) {
										nodesHospitals[i][4] = fmt.Sprintf("%d", firstNode.ID)
									}

									if nearestDistance > calcDist(Nodes[osm.NodeID(hospitalNodeID)], Nodes[nodeID]) {
										nodesHospitals[i][4] = fmt.Sprintf("%d", Nodes[nodeID].ID)
									}
								}
							}
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

	// This part only writes to a csv file
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

func calcDist(aNode, bNode osm.Node) float64 {
	return distance(aNode.Lat, aNode.Lon, bNode.Lat, bNode.Lon)

}

// Distance function returns the distance (in meters) between two points of
//     a given longitude and latitude relatively accurately (using a spherical
//     approximation of the Earth) through the Haversin Distance Formula for
//     great arc distance on a sphere with accuracy for small distances
//
// point coordinates are supplied in degrees and converted into rad. in the func
//
// distance returned is METERS!!!!!!
// http://en.wikipedia.org/wiki/Haversine_formula
func distance(lat1, lon1, lat2, lon2 float64) float64 {
	// convert to radians
	// must cast radius as float to multiply later
	var la1, lo1, la2, lo2, r float64
	la1 = lat1 * math.Pi / 180
	lo1 = lon1 * math.Pi / 180
	la2 = lat2 * math.Pi / 180
	lo2 = lon2 * math.Pi / 180

	r = 6378100 // Earth radius in METERS

	// calculate
	h := hsin(la2-la1) + math.Cos(la1)*math.Cos(la2)*hsin(lo2-lo1)

	return 2 * r * math.Asin(math.Sqrt(h))
}

// haversin(θ) function
func hsin(theta float64) float64 {
	return math.Pow(math.Sin(theta/2), 2)
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
