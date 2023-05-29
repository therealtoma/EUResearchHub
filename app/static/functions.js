
// Select Upload-Area
const uploadArea = document.querySelector('#uploadArea')
const uploadArea2 = document.querySelector('#uploadArea2')
// Select Drop-Zoon Area
const dropZoon = document.querySelector('#dropZoon');
const dropZoon2 = document.querySelector('#dropZoon2');
// Loading Text
const loadingText = document.querySelector('#loadingText');
const loadingText2 = document.querySelector('#loadingText2');
// Slect File Input
const fileInput = document.querySelector('#fileInput');
const fileInput2 = document.querySelector('#fileInput2');
fileInput.setAttribute('accept', 'image/*, application/pdf');
// Select Preview Image
const previewImage = document.querySelector('#previewImage');
const previewImage2 = document.querySelector('#previewImage2');
// File-Details Area
const fileDetails = document.querySelector('#fileDetails');
const fileDetails2 = document.querySelector('#fileDetails2');
// Uploaded File
const uploadedFile = document.querySelector('#uploadedFile');
const uploadedFile2 = document.querySelector('#uploadedFile2');
// Uploaded File Info
const uploadedFileInfo = document.querySelector('#uploadedFileInfo');
const uploadedFileInfo2 = document.querySelector('#uploadedFileInfo2');
// Uploaded File  Name
const uploadedFileName = document.querySelector('.uploaded-file__name');
const uploadedFileName2 = document.querySelector('.uploaded-file__name2');
// Uploaded File Icon
const uploadedFileIconText = document.querySelector('.uploaded-file__icon-text');
const uploadedFileIconText2 = document.querySelector('.uploaded-file__icon-text2');
// Uploaded File Counter
const uploadedFileCounter = document.querySelector('.uploaded-file__counter');
const uploadedFileCounter2 = document.querySelector('.uploaded-file__counter2');
// ToolTip Data
const toolTipData = document.querySelector('.upload-area__tooltip-data');
const toolTipData2 = document.querySelector('.upload-area__tooltip-data2');
// Images Types
const imagesTypes = [
    "jpeg",
    "png",
    "svg",
    "gif"
];
const imagesTypes2 = [
    "jpeg",
    "png",
    "svg",
    "gif"
];
// Append Images Types Array Inisde Tooltip Data
toolTipData.innerHTML = [...imagesTypes].join(', .');
toolTipData2.innerHTML = [...imagesTypes2].join(', .');

// When (drop-zoon) has (dragover) Event
dropZoon.addEventListener('dragover', function (event) {
    event.preventDefault();
    dropZoon.classList.add('drop-zoon--over');
});
dropZoon2.addEventListener('dragover', function (event) {
    // Prevent Default Behavior
    event.preventDefault();
    // Add Class (drop-zoon--over) On (drop-zoon)
    dropZoon2.classList.add('drop-zoon--over');
});

// When (drop-zoon) has (dragleave) Event
dropZoon.addEventListener('dragleave', function (event) {
    // Remove Class (drop-zoon--over) from (drop-zoon)
    dropZoon.classList.remove('drop-zoon--over');
});
dropZoon2.addEventListener('dragleave', function (event) {
    // Remove Class (drop-zoon--over) from (drop-zoon)
    dropZoon2.classList.remove('drop-zoon--over');
});

// When (drop-zoon) has (drop) Event
dropZoon.addEventListener('drop', function (event) {
    event.preventDefault();
    // Remove Class (drop-zoon--over) from (drop-zoon)
    dropZoon.classList.remove('drop-zoon--over');
    // Select The Dropped File
    const file = event.dataTransfer.files[0];
    // Call Function uploadFile(), And Send To Her The Dropped File :)
    uploadFile(file);
});
dropZoon2.addEventListener('drop', function (event) {
    // Prevent Default Behavior
    event.preventDefault();
    // Remove Class (drop-zoon--over) from (drop-zoon)
    dropZoon2.classList.remove('drop-zoon--over');
    // Select The Dropped File
    const file = event.dataTransfer.files[0];
    // Call Function uploadFile(), And Send To Her The Dropped File :)
    uploadFile2(file);
});


// When (drop-zoon) has (click) Event
dropZoon.addEventListener('click', function (event) {
    // Click The (fileInput)
    fileInput.click();
});
dropZoon2.addEventListener('click', function (event) {
    // Click The (fileInput)
    fileInput2.click();
});

// When (fileInput) has (change) Event
fileInput.addEventListener('change', function (event) {
    // Select The Chosen File
    const file = event.target.files[0];
    // Call Function uploadFile(), And Send To Her The Chosen File :)
    uploadFile2(file);
});
fileInput2.addEventListener('change', function (event) {
    // Select The Chosen File
    const file = event.target.files[0];
    // Call Function uploadFile(), And Send To Her The Chosen File :)
    uploadFile2(file);
});

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


/* SECOND INPUT */
function uploadFile2(file) {
    const fileReader2 = new FileReader();
    const fileType2 = file.type;
    const fileSize2 = file.size;
    if (fileValidate(fileType2, fileSize2)) {
        dropZoon2.classList.add('drop-zoon--Uploaded');
        loadingText2.style.display = "block";
        previewImage2.style.display = 'none';
        uploadedFile2.classList.remove('uploaded-file--open');
        uploadedFileInfo2.classList.remove('uploaded-file__info--active');
        if (fileType2 === 'application/pdf') {
            pdfToImage(file, function(imageData) {
                const image2 = new Image();
                image2.src = imageData;
                image2.onload = function() {
                    console.log('Object URL created:', image2.src);
                    previewImage2.setAttribute('src', image2.src);
                    previewImage2.style.display = 'block'; // Aggiungi questa linea per mostrare l'anteprima dell'immagine
                };
            }, function() {
                // After PDF to image conversion is complete
                // Add the necessary code here, if needed
                // Dopo la conversione del PDF in immagine è completata
                // Aggiungi qui il codice necessario, se necessario
                uploadArea2.classList.add('upload-area--open');
                loadingText2.style.display = "none";
                fileDetails2.classList.add('file-details--open');
                uploadedFile2.classList.add('uploaded-file--open');
                uploadedFileInfo2.classList.add('uploaded-file__info--active');
                progressMove2();
            });
        } else {
            fileReader2.addEventListener('load', function () {
                setTimeout(function () {
                    uploadArea2.classList.add('upload-area--open');
                    loadingText2.style.display = "none";
                    previewImage2.style.display = 'block';
                    fileDetails2.classList.add('file-details--open');
                    uploadedFile2.classList.add('uploaded-file--open');
                    uploadedFileInfo2.classList.add('uploaded-file__info--active');
                }, 500);
                previewImage2.setAttribute('src', fileReader2.result);
                uploadedFileName2.innerHTML = file.name;
                progressMove2();
            });
            fileReader2.readAsDataURL(file);
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
function progressMove2() {
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
                uploadedFileCounter2.innerHTML = `${counter}%`
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