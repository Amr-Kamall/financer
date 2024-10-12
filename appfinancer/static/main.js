document.addEventListener("DOMContentLoaded", function () {
  const imageInput = document.querySelector(".custum-file-upload");
  const imagePreview = document.querySelector(".icon");
  // Add event listener to input file change
  imageInput.addEventListener("change", function (e) {
    const file = e.target.files[0];
    if (!file) {
      imagePreview.innerHTML = "<p>No image picked yet</p>";
      return;
    }
    if (file.type.startsWith("image/")) {
      const reader = new FileReader();
      reader.onload = function (e) {
        imagePreview.innerHTML = `
                <img src="${e.target.result}" alt="the image selected by the user" />`;
      };
      reader.readAsDataURL(file);
    }
  });
});

// const noteText = document.querySelectorAll(".note-text");

// const looped = noteText.forEach((ele) => {
//   console.log(ele.innerHTML);
//   ele.innerHTML.length > 12
//     ? ele.classList.add("break-text")
//     : console.log("amr kamal ");
// });
//
