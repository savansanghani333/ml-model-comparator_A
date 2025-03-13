function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const loader = document.querySelector(".loader");
    const resultsTable = document.getElementById("resultsTable");
    const tbody = resultsTable.querySelector("tbody");

    if (fileInput.files.length === 0) {
        alert("Please select a CSV file.");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    loader.style.display = "block";
    resultsTable.style.display = "none";

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loader.style.display = "none";
        resultsTable.style.display = "table";
        tbody.innerHTML = "";

        let bestModel = data["Best Model"];
        let bestAccuracy = data["Best Accuracy"];

        Object.keys(data).forEach(model => {
            if (model !== "Best Model" && model !== "Best Accuracy") {
                let row = document.createElement("tr");
                row.innerHTML = `<td>${model}</td><td>${data[model]}</td>`;
                if (model === bestModel) {
                    row.classList.add("highlight");
                }
                tbody.appendChild(row);
            }
        });
    })
    .catch(error => {
        loader.style.display = "none";
        alert("Error processing file. Please try again.");
    });
}
