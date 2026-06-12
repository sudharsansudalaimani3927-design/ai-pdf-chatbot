let pdfReady = false;

    async function uploadPDF(){
        const file =
            document.getElementById("pdf").files[0];

        if(!file){
            alert("Please select a PDF");
            return;
        }

        pdfReady = false;

        document.getElementById("askBtn").disabled = true;

        document.getElementById("askBtn").innerText = 
            "Processing PDF...";

        document.getElementById("uploadResult").innerHTML =
            "🚀 Starting upload...";

        document.getElementById("processTracker").innerHTML =
            "";

        const formData = new FormData();
        formData.append("file", file);

        const statusInterval = setInterval(
            async () => {

                try{

                    const response =
                        await fetch("/status");

                    const data =
                        await response.json();

                    document.getElementById(
                        "processTracker"
                    ).innerHTML =
                        data.status;

                    if(
                        data.status.includes("Completed")
                    ){

                        clearInterval(
                            statusInterval
                        );

                    }

                }

                catch(error){
                    console.log(error);
                }

            },

            500
        );

        try{

            const response =
                await fetch(
                    "/upload",
                    {
                        method:"POST",
                        body:formData
                    }
                );

            const data =
                await response.json();

            pdfReady = true;

            document.getElementById(
                "askBtn"
            ).disabled = false;

            document.getElementById(
                "askBtn"
            ).innerText =
                "Ask";

            document.getElementById(
                "uploadResult"
            ).innerHTML =

            `
            ✅ PDF Processed Successfully
            <br>
            📦 Chunks Generated:
            ${data.chunks}
            `;

        }

        catch(error){

            console.error(error);

            document.getElementById(
                "uploadResult"
            ).innerHTML =

            "❌ Upload Failed";

        }

    }
    async function askQuestion(){

    if(!pdfReady){

        alert("Please upload a PDF first.");
        return;

    }

    const question =
        document.getElementById(
            "question"
        ).value.trim();

    if(!question){

        alert("Enter a question");
        return;

    }

    const chatContainer =
        document.getElementById(
            "chatContainer"
        );

    // User Message

    chatContainer.innerHTML += `
        <div class="d-flex justify-content-end mb-3">

            <div
                class="bg-primary text-white p-3 rounded w-75"
            >

                <strong>You</strong>

                <hr>

                ${question}

            </div>

        </div>
    `;

    // Thinking Message

    chatContainer.innerHTML += `
        <div
            id="thinking"
            class="d-flex justify-content-start mb-3"
        >

            <div
                class="bg-secondary text-white p-3 rounded w-75"
            >

                <div
                    class="spinner-border spinner-border-sm me-2"
                    role="status"
                ></div>

                Thinking...

            </div>

        </div>
    `;

    chatContainer.scrollTop =
        chatContainer.scrollHeight;

    document.getElementById(
        "question"
    ).value = "";

    try{

        const response =
            await fetch(
                "/ask",
                {
                    method:"POST",

                    headers:{
                        "Content-Type":
                        "application/json"
                    },

                    body:JSON.stringify({
                        question:question
                    })
                }
            );

        const data =
            await response.json();

        // Remove Thinking Bubble

        const thinking =
            document.getElementById(
                "thinking"
            );

        if(thinking){

            thinking.remove();

        }

        let sourceHTML = "";

        if(
            data.sources &&
            data.sources.length > 0
        ){

            for(
                let i = 0;
                i < data.sources.length;
                i++
            ){

                sourceHTML += `
                    <div
                        class="card bg-dark border-primary mt-2"
                    >

                        <div class="card-body">

                            <small>

                                ${data.sources[i]}

                            </small>

                        </div>

                    </div>
                `;
            }

        }

        // AI Message

        chatContainer.innerHTML += `
            <div
                class="d-flex justify-content-start mb-3"
            >

                <div
                    class="bg-secondary text-white p-3 rounded w-75"
                >

                    <strong>AI</strong>

                    <hr>

                    ${data.answer}

                    <div class="mt-3">

                        <strong>
                            📚 Sources
                        </strong>

                        ${sourceHTML}

                    </div>

                </div>

            </div>
        `;

        chatContainer.scrollTop =
            chatContainer.scrollHeight;

    }

    catch(error){

        console.error(error);

        const thinking =
            document.getElementById(
                "thinking"
            );

        if(thinking){

            thinking.remove();

        }

        chatContainer.innerHTML += `
            <div
                class="d-flex justify-content-start mb-3"
            >

                <div
                    class="bg-danger text-white p-3 rounded w-75"
                >

                    ❌ Failed to generate answer

                </div>

            </div>
        `;

    }

}
    

