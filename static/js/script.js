document.getElementById('uploadForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Ngăn không cho trang tải lại

    const formData = new FormData(this);
    
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(result => {
        document.getElementById('result').innerText = result; // Hiển thị kết quả

        // Hiển thị hình ảnh đã tải lên
        const fileInput = document.querySelector('input[type="file"]');
        const file = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            const imgElement = document.getElementById('uploadedImage');
            imgElement.src = e.target.result; // Cập nhật src với nội dung của file
            imgElement.style.display = 'block'; // Hiện hình ảnh
        };

        reader.readAsDataURL(file); // Đọc file hình ảnh
    })
    .catch(error => {
        console.error('Lỗi:', error);
        document.getElementById('result').innerText = "Đã xảy ra lỗi khi gửi yêu cầu.";
    });
});
