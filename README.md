# MCSW-Project


<h3> Movie aggregation project</h2><br>

Team members: <br>
<ol>
  <li>Toc Sebastian George</li>
</ol> 

Project Steps:<br>

<h2>#O1</h2><br>
Packages needed:<br>
 <ul>
  <li>extruct -> pip3 install extruct</li>
  <li>requests -> pip3 install requests</li>
  <li>w3lib -> pip3 install w3lib</li>
</ul> 

Description: <br>
<ol>
  <li>Implements the DataExtraction class from the DataExtraction.py file</li>
  <li>DataExtraction class is used to extract the metadata from IMDb and with it, we can extract the info about movies from that website. The metadata contains the Schema.org info about that specific movie and after the class extracts it, the class also parses that metadata and finds the information about that movie ( name, rating, number of votes, actors, director and so on)</li>
  <li>DataExtraction class is initialized with a list of URLs to different movies from IMDb, and after it extracts the info about each movie it returns a list of Movie objects. the Movie class is used to define how a movie should look like.</li>

</ol> 


<h2>#O2</h2><br>
Packages needed:<br>
 <ul>
  <li>rdflib -> pip3 install rdflib</li>
</ul> 

Description: <br>
<ol>
  <li>MovieDB class is implemented</li>
  <li>The MovieDB class is used to convert the Movie objects from the previous step in RDF and stores them in a TTL
  (turtle) file which will be used as a small database on our local machine</li>
  <li>The class appends new movies to the database file </li>
</ol> 

<h2>#O3</h2><br>
Description: <br>
<ol>
  <li>The MovieDB class is used also in this step.</li>
  <li>The TTL file is loaded in the memory and then SPARQL queries are ran in order to get the desired info about a movie</li>
  <li>The class is used to retrieve the data and also provides some filters that the user can use. </li>
</ol> 
</ol> 


      
