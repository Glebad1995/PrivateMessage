    const fileInput = document.getElementById('file');
    const fileList = document.getElementById('file-list');

    fileInput.addEventListener('change', handleFileSelect);

    function handleFileSelect(event) {
        fileList.innerHTML = '';

        const files = event.target.files;

        for (let i = 0; i < files.length; i++) {
            const file = files[i];

            const fileItem = document.createElement('div');
            fileItem.classList.add('file-item');

            const fileName = document.createElement('span');
            fileName.classList.add('file-name');
            fileName.textContent = file.name;

            const fileRemove = document.createElement('span');
            fileRemove.classList.add('file-remove');
            fileRemove.textContent = 'Delete';
            fileRemove.addEventListener('click', removeFile.bind(null, fileItem));

            fileItem.appendChild(fileName);
            fileItem.appendChild(fileRemove);
            fileList.appendChild(fileItem);
        }
    }

    function removeFile(fileItem) {
        fileItem.remove();
    }
    function copyLink() {
        var linkInput = document.getElementById('link-input');
        linkInput.select();
        linkInput.setSelectionRange(0, 99999);
        document.execCommand("copy");

        var copyText = document.getElementById('copy-text');
        copyText.style.opacity = "1";
        copyText.style.visibility = "visible";

        setTimeout(function () {
            copyText.style.opacity = "0";
            setTimeout(function () {
                copyText.style.visibility = "hidden";
            }, 500);
        }, 3000);
    }