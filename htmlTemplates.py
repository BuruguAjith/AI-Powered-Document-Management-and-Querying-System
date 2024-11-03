<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Planet</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h3 {
            font-size: 25px;
            color: #333;
        }
        .sidebar {
            float: left;
            width: 30%;
            padding: 15px;
            background-color: #f9f9f9;
            border-right: 1px solid #ddd;
            height: 100vh;
        }
        .content {
            float: right;
            width: 65%;
            padding: 15px;
        }
        .button {
            padding: 10px 15px;
            font-size: 16px;
            color: white;
            background-color: #007bff;
            border: none;
            cursor: pointer;
        }
        .button:hover {
            background-color: #0056b3;
        }
        .input-field, .upload-field {
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <h2>Menu:</h2>
            <div class="upload-field">
                <label for="pdf-upload">Upload your PDF Files</label>
                <input type="file" id="pdf-upload" multiple>
            </div>
            <button class="button" onclick="processFiles()">Submit & Process</button>
            <p id="status"></p>
        </div>
        
        <div class="content">
            <h3>Please ask your question to AI Planet 🌍</h3>
            <div class="input-field">
                <input type="text" id="question" placeholder="Type your question here" style="width: 100%; padding: 10px;">
            </div>
            <button class="button" onclick="askQuestion()">Submit</button>
            <div id="response"></div>
        </div>
    </div>

    <script>
        function processFiles() {
            const status = document.getElementById("status");
            status.innerText = "Processing...";
            
            // Simulate processing and response
            setTimeout(() => {
                status.innerText = "Processing complete!";
            }, 2000);
        }

        function askQuestion() {
            const question = document.getElementById("question").value;
            const response = document.getElementById("response");

            if (question) {
                // Simulate an AI response
                response.innerHTML = "<p><strong>Reply:</strong> AI-generated answer will appear here.</p>";
            } else {
                response.innerHTML = "<p>Please enter a question.</p>";
            }
        }
    </script>
</body>
</html>
