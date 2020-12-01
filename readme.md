**Pan card Data Extractor** `flask` `OCR Api`
<br>
The program is to extract the name, date of birth and pan card number from PAN card image.
Program is written using FLASK python framework and using https://api.ocr.space/parse/image api for running OCR on image. <br>
The ui of the application is designed using bootstrap which is linked using cdn. All the templates
of the application is located at the template directory. 

**Running the Application**<br>
The libraries are installed in python virtual environment(venv). The main file of application is 
`app.py` which will run the server on port 5000 so in any case if it is already occupied please change the 
port in the app.py. <br>
Before running the application make sure that the virtual environment venv is activated if it is not please
activate using `.\env\Scripts\activate` on windows and `source env/bin/activate` on mac and linux.
You can run the application using `python3 app.py`.<br>
The url of the application is http://127.0.0.1:5000/ running on localhost. The ocr application
is available in this default end point. After selecting a pan card image you can click the
submit button to view the extracted information on browser.

