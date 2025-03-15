function getRecommendations() {
    let materialType = document.getElementById("material_type").value;
    let recyclable = document.getElementById("recyclable").value;
    let compostable = document.getElementById("compostable").value;

    let url = "/recommend?";
    if (materialType) url += `material_type=${encodeURIComponent(materialType)}&`;
    if (recyclable) url += `recyclable=${recyclable}&`;
    if (compostable) url += `compostable=${compostable}&`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            let results = document.getElementById("results");
            results.innerHTML = "";

            if (data.length === 0) {
                results.innerHTML = "<li>No recommendations found.</li>";
            } else {
                data.forEach(item => {
                    let li = document.createElement("li");
                    li.textContent = `${item["Material Type"]} - Recyclable: ${item["Recyclable"]}, Compostable: ${item["Compostable"]}`;
                    results.appendChild(li);
                });
            }
        })
        .catch(error => console.error("Error fetching recommendations:", error));
}
