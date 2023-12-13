# matapp

### Description
The app performs application of materials to 3D objects and generates .glb (binary gltf) at output.
Input type of objects: *.usd (after POST request it puts *.usd files to data/input)
Output type of objects: *.glb (after processing the object with applied materials will be at the data.output folder)

### Simple case - one material for a whole object
The case when we have an object and we apply single (specified in request) material.
The script takes POST request with *.usd model and material (as a string), applies regarding material to the object in Blender and outputs it as *.glb file. 


### Installation
* Blender file with materials - the blender scene with no objects with materials (will be fed with docker-compose.yml):
  * Silver
  * Rose Gold
  * White Gold
  * Yellow Gold
  * Palladium
  * Black Rhodium
* Build container with ```docker build -t matapp .```
* Run the container with ```docker-compose up -d```
* The endpoint at the specified in *docker-compose.yml* address and port
* Get output at ./data/output