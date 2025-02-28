function performSearch() {
    var query = document.getElementById("search-query").value;
    var method = document.getElementById("search-method").value;

    fetch("/search", {
	method: "POST",
	headers: {"Content-Type": "application/json"},
	body: JSON.stringify({query: query, method: method})
    })
	.then(response => response.json())
    
	.then(data => {
	    let resultsList = document.getElementById("results");
	    resultsList.innerHTML = "";
	    
	    data.forEach(result => {
		let li = document.createElement("li");
		li.textContent = result;
		result.appendChild(li);
	    });
	});

    return result;
}
	    
