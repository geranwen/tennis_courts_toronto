# Tennis courts within the City of Toronto

The public website provided by the city can be hard to use, since it did not provide the full address and did not show the locations on any map. 

On the other hand, the map-view did not provide enough details about the courts, making the selection process difficult. 

The 2 reasons listed above prompted me into making this simple project: a website where you can search for and evaluate your tennis court options. In addition to text-based search, users can also filter by number of courts, availability of lights at night, public vs club courts, accessibility during winter, etc. 

The website can be found [here](https://trt-tennis-map.herokuapp.com/).

### Notes:
- The data collection process was taken care of by a separate Jupyter notebook, with some manual verification & adjustments. The notebook `data_grab.ipynb` can be found in the mvp branch. The idea of extracting data from source (toronto.ca) was considered, but deemed unecessarily complicated because information on tennis courts won't frequently change. 


### Next steps:
1. ~~At the moment, the filters need to be implemented in code. The intention in the future is to create a simple GUI for ease of use, hosted on a simple website. This will be the main objective for the next phase of this project.~~
2. ~~Fix csv database to improve accuracy.~~
3. Improved search feature that allows fuzzy matching with tolarence for skipped workds, and possibly return top x matches, or matches that's above a certain quality threshold. 
4. ~~Implement filter by conditions (winter, lights, public/club, etc.)~~
5. Overlay public transportation options & bike share stations. (not straight forward, which is why it will be given lower priority)


### Acknowledgement

This project utilizes data provided by the City of Toronto under the Open Government Licence – Toronto. The data used pertains to the locations of tennis courts in the city. The original dataset can be accessed [here](https://www.toronto.ca/data/parks/prd/facilities/tennis/index.html).

We would like to express our gratitude to the City of Toronto for making this data available for public use. By providing this data, the City of Toronto supports open government principles and enables citizens to engage with their city in new and innovative ways.