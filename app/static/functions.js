

// Design By
// - https://dribbble.com/shots/13992184-File-Uploader-Drag-Drop

// Select Upload-Area
const uploadArea = document.querySelector('#uploadArea')

// Select Drop-Zoon Area
const dropZoon = document.querySelector('#dropZoon');

// Loading Text
const loadingText = document.querySelector('#loadingText');

// Slect File Input
const fileInput = document.querySelector('#fileInput');
fileInput.setAttribute('accept', 'image/*, application/pdf');

// Select Preview Image
const previewImage = document.querySelector('#previewImage');

// File-Details Area
const fileDetails = document.querySelector('#fileDetails');

// Uploaded File
const uploadedFile = document.querySelector('#uploadedFile');

// Uploaded File Info
const uploadedFileInfo = document.querySelector('#uploadedFileInfo');

// Uploaded File  Name
const uploadedFileName = document.querySelector('.uploaded-file__name');

// Uploaded File Icon
const uploadedFileIconText = document.querySelector('.uploaded-file__icon-text');

// Uploaded File Counter
const uploadedFileCounter = document.querySelector('.uploaded-file__counter');

// ToolTip Data
const toolTipData = document.querySelector('.upload-area__tooltip-data');

// Images Types
const imagesTypes = [
    "jpeg",
    "png",
    "svg",
    "gif"
];

// Append Images Types Array Inisde Tooltip Data
toolTipData.innerHTML = [...imagesTypes].join(', .');

// When (drop-zoon) has (dragover) Event
dropZoon.addEventListener('dragover', function (event) {
    // Prevent Default Behavior
    event.preventDefault();

    // Add Class (drop-zoon--over) On (drop-zoon)
    dropZoon.classList.add('drop-zoon--over');
});

// When (drop-zoon) has (dragleave) Event
dropZoon.addEventListener('dragleave', function (event) {
    // Remove Class (drop-zoon--over) from (drop-zoon)
    dropZoon.classList.remove('drop-zoon--over');
});

// When (drop-zoon) has (drop) Event
dropZoon.addEventListener('drop', function (event) {
    // Prevent Default Behavior
    event.preventDefault();

    // Remove Class (drop-zoon--over) from (drop-zoon)
    dropZoon.classList.remove('drop-zoon--over');

    // Select The Dropped File
    const file = event.dataTransfer.files[0];

    // Call Function uploadFile(), And Send To Her The Dropped File :)
    uploadFile(file);
});

// When (drop-zoon) has (click) Event
dropZoon.addEventListener('click', function (event) {
    // Click The (fileInput)
    fileInput.click();
});

// When (fileInput) has (change) Event
fileInput.addEventListener('change', function (event) {
    // Select The Chosen File
    const file = event.target.files[0];

    // Call Function uploadFile(), And Send To Her The Chosen File :)
    uploadFile(file);
});




function pdfToImage(file, imageCallback, completeCallback) {
    const fileReader = new FileReader();
    fileReader.onload = function() {
        const typedarray = new Uint8Array(this.result);
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.8.335/pdf.worker.min.js';

        pdfjsLib.getDocument(typedarray).promise.then(function(pdf) {
            pdf.getPage(1).then(function(page) {
                const viewport = page.getViewport({ scale: 1 });
                const canvas = document.createElement('canvas');
                canvas.width = viewport.width;
                canvas.height = viewport.height;
                const context = canvas.getContext('2d');

                const renderContext = {
                    canvasContext: context,
                    viewport: viewport
                };

                page.render(renderContext).promise.then(function() {
                    const imageData = canvas.toDataURL('image/png');
                    imageCallback(imageData);
                    completeCallback();
                });
            });
        });
    };
    fileReader.readAsArrayBuffer(file);
}


// Upload File Function
function uploadFile(file) {
    const fileReader = new FileReader();
    const fileType = file.type;
    const fileSize = file.size;

    if (fileValidate(fileType, fileSize)) {
        dropZoon.classList.add('drop-zoon--Uploaded');
        loadingText.style.display = "block";
        previewImage.style.display = 'none';
        uploadedFile.classList.remove('uploaded-file--open');
        uploadedFileInfo.classList.remove('uploaded-file__info--active');

        if (fileType === 'application/pdf') {
            pdfToImage(file, function(imageData) {
                const image = new Image();
                image.src = imageData;
                image.onload = function() {
                    console.log('Object URL created:', image.src);
                    previewImage.setAttribute('src', image.src);
                    previewImage.style.display = 'block'; // Aggiungi questa linea per mostrare l'anteprima dell'immagine
                };
            }, function() {
                // After PDF to image conversion is complete
                // Add the necessary code here, if needed

                // Dopo la conversione del PDF in immagine è completata
                // Aggiungi qui il codice necessario, se necessario
                uploadArea.classList.add('upload-area--open');
                loadingText.style.display = "none";
                fileDetails.classList.add('file-details--open');
                uploadedFile.classList.add('uploaded-file--open');
                uploadedFileInfo.classList.add('uploaded-file__info--active');
                progressMove();
            });
        } else {
            fileReader.addEventListener('load', function () {
                setTimeout(function () {
                    uploadArea.classList.add('upload-area--open');
                    loadingText.style.display = "none";
                    previewImage.style.display = 'block';
                    fileDetails.classList.add('file-details--open');
                    uploadedFile.classList.add('uploaded-file--open');
                    uploadedFileInfo.classList.add('uploaded-file__info--active');
                }, 500);

                previewImage.setAttribute('src', fileReader.result);
                uploadedFileName.innerHTML = file.name;
                progressMove();
            });

            fileReader.readAsDataURL(file);
        }
    } else {
        // Add the necessary code for file validation failure, if needed
    }
}


// Progress Counter Increase Function
function progressMove() {
    // Counter Start
    let counter = 0;

    // After 600ms
    setTimeout(() => {
        // Every 100ms
        let counterIncrease = setInterval(() => {
            // If (counter) is equle 100
            if (counter === 100) {
                // Stop (Counter Increase)
                clearInterval(counterIncrease);
            } else { // Else
                // plus 10 on counter
                counter = counter + 10;
                // add (counter) vlaue inisde (uploadedFileCounter)
                uploadedFileCounter.innerHTML = `${counter}%`
            }
        }, 100);
    }, 600);
};


// Simple File Validate Function
function fileValidate(fileType, fileSize) {
    // File Type Validation
    let isImage = imagesTypes.filter((type) => fileType.indexOf(`image/${type}`) !== -1);

    // If the uploaded file is an image or PDF
    if (isImage.length !== 0 || fileType === 'application/pdf') {
        // Check if the file size is 2MB or less
        if (fileSize <= 2000000) { // 2MB
            return true;
        } else {
            alert('Please ensure your file size is 2 Megabytes or less.');
            return false;
        }
    } else {
        alert('Please make sure to upload an image or PDF file.');
        return false;
    }
}


// :)