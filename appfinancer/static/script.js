const signUpButton = document.getElementById("signUp");
const signInButton = document.getElementById("signIn");
const container = document.getElementById("container");

signUpButton.addEventListener("click", () => {
  container.classList.add("right-panel-active");
});

signInButton.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
});

// my new functionality

const signupContainer = document.querySelector(".sign-up-container");
const signinContainer = document.querySelector(".sign-in-container");
const formContainer = document.querySelector(".form-container");
const loginBtn = document.querySelector(".btn-login");
const resBtn = document.querySelector(".btn-resposible");

resBtn.addEventListener("click", function () {
  signupContainer.style.cssText = `
    z-index:0;
    transform: translateX(100%)
  `;
  signinContainer.style.cssText = `
    transform: translateX(0)
  `;
});

loginBtn.addEventListener("click", function () {
  signupContainer.style.cssText = `
    left: 114px;
    min-width: 90%;
    opacity: 10;
    z-index: 1000;
    position: absolute;
    inset: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    width:100%;
    transform: translateX(0px);
  `;
});

//  form{   transform: translateX(370px);}
