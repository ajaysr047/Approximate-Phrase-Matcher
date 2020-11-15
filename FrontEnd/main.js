const addOrView = document.getElementById('add/view');
const slide = document.getElementById('slide');
const container = document.getElementById('container');

addOrView.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

slide.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
	document.getElementById("isPosted").innerHTML = "";
});

// https://extracttags.herokuapp.com/

document.getElementById("addNewTag").onclick = function () {

var settings = {
	"url": "http://127.0.0.1:5000/addTag",
	"method": "POST",
	"timeout": 0,
	"headers": {
		"Content-Type": "application/json"
	},
	"data": JSON.stringify({"Tag": document.getElementById("newTag").value}),
	};
	
	$.ajax(settings).done(function (response) {
		
		if(response.isPosted)
		{
			document.getElementById("isPosted").innerHTML = "Tag Successfully added!!";
			var settings2 = {
				"url": "http://127.0.0.1:5000/getAllTags",
				"method": "GET",
				"timeout": 0,
				"headers": {
				  "Content-Type": "application/json"
				},
			  };
			  
			  $.ajax(settings2).done(function (response) {
				if(response.isFetched && response.Tags.length > 0)
					document.getElementById("availableTags").innerHTML = "Available Tags: " + response.Tags.join();
				else
					document.getElementById("availableTags").innerHTML = "No tags available!!"
			  });
		}
		else
			document.getElementById("isPosted").innerHTML = "Tag not added!!";
	});
};

document.getElementById("find").onclick = function () {

	var settings = {
		"url": "http://127.0.0.1:5000/extractTags",
		"method": "POST",
		"timeout": 0,
		"headers": {
			"Content-Type": "application/json"
		},
		"data": JSON.stringify({"query": document.getElementById("inputText").value}),
		};
		
		$.ajax(settings).done(function (response) {
			if(response.isSuccess)
				document.getElementById("foundTags").innerHTML = "Found Tags: " + response.Tags.join();
			else
				document.getElementById("foundTags").innerHTML = "No Tags found!!";
		});
};


document.getElementById("add/view").onclick = function () {

	var settings = {
		"url": "http://127.0.0.1:5000/getAllTags",
		"method": "GET",
		"timeout": 0,
		"headers": {
		  "Content-Type": "application/json"
		},
	  };
	  
	  $.ajax(settings).done(function (response) {
		  console.log(response.Tags.length)
		if(response.isFetched && response.Tags.length > 0)
			document.getElementById("availableTags").innerHTML = "Available Tags: " + response.Tags.join();
		else
			document.getElementById("availableTags").innerHTML = "No tags available!!"
	  });
};

/*
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]
spacy = "*"
pandas = "*"
fuzzywuzzy = "*"
nltk = "*"
flask = "*"
flask-cors = "*"
flask-pymongo = "*"
dnspython = "*"
python-levenshtein = "*"

[requires]
python_version = "3.8"

*/