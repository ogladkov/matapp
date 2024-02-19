# matapp

### Description
The app performs application of materials to 3D objects and generates .glb (binary gltf) at output.
Input type of objects: *.usd (after POST request it puts *.usd files to data/input)
Output type of objects: *.glb (after processing the object with applied materials will be at the data.output folder)

### Simple case - one material for a whole object
##### Endpoint: ./simple_apply/
The case when we have an object and we apply single (specified in request) material.
The script takes POST request with *.usd model and material (as a string), applies regarding material to the object in Blender and outputs it as *.glb file. 

### Multimaterial case - stone and metal materials apply to different object
##### Endpoint: ./cls_apply/
In this case the uploaded object will be classified (mesh-wise) with two classes ('stone' and 'metal'). Materials (materials ids specify in request with integers) will be applied according the classification.
Finally the object will be exported to .gltf to **./data/output** folder.

### Manual correction case - fix the mistake of the classifying NN'
##### Endpoint: ./corrected_apply/
In the case of wrong prediction of the material for a mesh (or meshes) in a model, you can open the gLTF (glb-file) in Blender
and manually add for the mesh name (*not object name!!*) the suffix: '_x_stone' or '_x_metal'. Aftrer that it is necessary 
to export the gLTF (glb) file overwriting the previous one in the folder './data/output'.
Now you can use the endpoint selecting materials again. The proper materials will be applied and you will get the result 
at the same gLTF (glb) file at './data/output/model.glb'

### Installation
* Blender file with materials - the blender scene with no objects with materials (will be fed with docker-compose.yml):
  * 1: Silver
  * 2: Rose Gold
  * 3: White Gold
  * 4: Yellow Gold
  * 5: Palladium
  * 6: Black Rhodium
  * 7: Emerald
  * 8: Ruby
  * 9: Sapphire
* Build container with ```docker build -t matapp .```
* Run the container with ```docker-compose up -d```
* The endpoint at the specified in *docker-compose.yml* address and port
* Get output at ./data/output