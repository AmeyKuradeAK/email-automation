async function uploadFiles() {
    const markdownFile = document.getElementById('markdownFile').files[0];
    const csvFile = document.getElementById('csvFile').files[0];

    if (!markdownFile || !csvFile) {
        alert("Please upload both Markdown and CSV files.");
        return;
    }

    const formData = new FormData();
    formData.append("markdown", markdownFile);
    formData.append("csv", csvFile);

    try {
        // Log request info before sending it
        console.log("Sending request to Flask API...");

        const response = await fetch("http://localhost:5000/upload", {
            method: "POST",
            body: formData,
            headers: {
                // Optional: you could set headers here if necessary, but not for FormData
            }
        });

        // Log the response
        console.log("Response received:", response);

        const result = await response.json();

        if (response.ok) {
            alert("Your Emails will be shortly uploaded! Thanks for your patience");
            console.log("Files uploaded successfully!");
            console.log("Markdown File Path:", result.markdown_file);
            console.log("CSV File Path:", result.csv_file);
        } else {
            console.error("Error Response:", result);
            alert("Error: " + result.error);
        }
    } catch (error) {
        console.error("Error during upload:", error);
        alert("An error occurred while uploading files. Check the console for details.");
    }
}
