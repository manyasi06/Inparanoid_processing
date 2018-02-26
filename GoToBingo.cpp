/**********************************************************************************************************************
Author: Bryan Musungu
Description: Take in a interpro file go information and convert to bingo format for cytoscape.
The data should Column1 containing the geneid seperated by a tab
*************************************************************************************************************************/


#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <regex>



bool fexists(const std::string& stringIn);


int main() {
	using namespace std;

	string stringIn;
	string stringOut;
	string value;
	string value2;
	regex re("\\s+|\\|");
	sregex_token_iterator reg_end;


	

	cout << "Input the name of the file: " << endl;
	getline(cin, stringIn);
	cout << "The output file name is " << endl;
	getline(cin, stringOut);
	
	
	ifstream inputFile(stringIn);
	ofstream outputFile(stringOut);

	

	//Lets the user know if the file exists
	if (!inputFile) {
			cout << "Cannot open input file" << endl;
		}

	if (!outputFile) {
		cout << "Can not save output file" << endl;
	}


	//It should iterate through the values using column and column2 delimited by the pipe sign.
	//For example GO:0005524|GO:0008026 and this could be of unknown length.
	while (getline(inputFile,value)) {
			sregex_token_iterator it(value.begin(), value.end(), re, -1);
			std::string p1 = (it++)->str();
			//std::cout << "This is P1: " << p1 << " and " << it->str() << std::endl;
			for (; it != reg_end; ++it) {
				std::string test = it->str();
				std::string test2 = test.substr(3, test.length());
				outputFile << p1 << " = " << test2 << endl;			

			}
				}


	outputFile.close();
	inputFile.close();
	cin.get();

	return 0;

}


/*
fexists(stringIn);
oexists(stringOut);
*/


/******************************************************************************************************************
	Purpose of this function is to check if the file exists.	
*******************************************************************************************************************/
	bool fexists(const std::string& fileIn) {
		using namespace std;
		
		ifstream inputFile(fileIn.c_str());
		return (bool)inputFile;
	
	}
	

	bool oexists(const std::string& fileIn2) {
		using namespace std;

		ofstream outputFile(fileIn2.c_str());
		return (bool)outputFile;

	}


	