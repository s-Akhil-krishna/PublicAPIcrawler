# PublicAPIcrawler
Crawl the data from the given API endpoint and store it in a database 

Pre-Docker steps:
    1.Download and install docker from https://www.docker.com/products/docker-desktop
    2.Test if the docker is working by the following cmds
        a. docker --version
        b. docker info
        c. docker run hello-world
    3. Troubleshooting: 
        a. Enable Hyper-V
        b. Save "Dockerfile" without extension. 

I. Steps to run the program
    1. Clone the project into local machine 
    2. Open up the powershell in administrative mode 
        a. cd into the project directory
        b. Run the command "docker build . -f Dockerfile -t crawler"
        c. If it builds the image succesfully, run "docker run crawler"
     Outputs:
        This presents the crawled data and displays in the form of data frames for each category
        "Successfully pushed to SQLite database" is displayed which means the data is pushed into a database



II. Language and tools used
    1.Language used: Python
      version :      3
      Description:   Python3 image pulled from docker-hub for this purpose, refer the Dockerfile
    
    2.Database used:  SQLite with SQLAlchemy
      Description:     SQLite is a inbuilt database supported by python.
    
    
III. Database Schema 
    The data is all similar, so we stored entire data in a single table.
    Columns/Attributes of the table are as follows. Table name = "model"
   
    Column           DataType  
    id               Integer
    api              String 
    description      String
    auth             String
    https            String 
    cors             String
    link             String 
    category         String
    
    Kindly refer the "Model" class of Sqlite_data.py to understand more about the model of the table.

IV. Points achieved
    1. Concept of OOPS
        a. The entire code is written in the form of classes and objects
        b. Followed some of best practices from PEP-8 guidelines :
            b1. structure of code 
            b2. naming conventions with meaningful names 
            b3. modularity: code split into 2 modules namely "Scraoe.py" & "Sqlite_data.py"
            b4. Tried to minimize global variables
            b5. Encapsulation - data is mostly used and transferred only inside the class members 
        c. DRY - Do not Repeat Yourself
            Tried to incorporate this principle into the code logic as much as possible.
    
    2. Support for handling athentication requirements & token expiration of server
        API : https://public-apis-api.herokuapp.com
        a. The tokens are obtained from https://public-apis-api.herokuapp.com/api/v1/auth/token
        b. Token expiry time: 5 minutes or 300 seconds
        meaning: We request for a new token every 5 minutes to authenticate the API.
        After obtaining the token, it is embedded into the header for any further API requests.
   
        Authorization: Bearer <token>
        Eg: Authorization: Bearer hdjfhsajlf;dolfkldjfskjfkdfjdhfshldfs
        Developed Solution: 
            A method get_token() uses a timer. 
           
     3. Support for Pagination
         a. There are 5 pages in total.
         b. For every page
              b1. API URL is updated
              b2. Make a authorized request 
              b3. crawl the data 
              b4. collect the data
     
     4. Work around for rate limited server
        a. The server accepts a maximum of 10 requests per minute
        Developed solution:
            when the server response status_code is other than 200,
            a.the crawler goes into sleep mode for a few seconds
            b. perform re-request 
      
     5.Crawl all API entries for all categories and store in a database
        The data is collected in the above methods 
        a. Created a database
        b. Created a schema/model for the table
        c. Pushed the data into the python SQLite database
    
    
    All the points are achieved and produces the desired results.
    
    A few observations:
    The given API return absolute zero entries for some categories.
    Responses received for such categories are stored in a data member empty_categories.
    
      
 V. Possible Improvements      
      1. There are a few different types of ways to creating,storing,retrieving from the database
          1a. Probably, we could see which is more readable, relatable for easy working. 
      2. DB CRUD operations can be effectively incorporated into the code
           Create, Retrieve, Update, Delete
      3. The assignment is focussed on crawling the top surface of the API.
          We could try to dig deeper into all the API links, if we need in-depth crawling.
      4. We can try to use any online crawlers that might give us better speed and memory.  
      5. We can make the code more genralized for similar APIs.     
       
           
        
  


