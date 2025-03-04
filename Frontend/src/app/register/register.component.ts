import { Component, OnInit } from '@angular/core';
import { AuthService } from '../_auth/services/auth.service';
import { Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  registerForm: FormGroup;

  processing: Boolean = false;
  error: Boolean = false;


  constructor(
    private authService: AuthService,
    private router: Router,
  ) { }


  ngOnInit() {
    if (this.authService.hasToken()) {
      this.handleLoginSuccess();
    } else {
      this.initForm();
    }
  }

  initForm() {
    this.registerForm = new FormGroup({
      email: new FormControl('', [ Validators.required, Validators.email]),
      password: new FormControl('', Validators.required),
      confirmPassword: new FormControl('', Validators.required),
    });
  }

  handleRegisterError() {
    this.processing = false;
    this.error  = true;
  }

  onSubmitButtonClicked() {
    this.error  = false;
    this.processing  = false;
    if (this.registerForm.valid && this.registerForm.get("password")?.value == this.registerForm.get("confirmPassword")?.value ) {
      this.register();
    }else{
      alert("Invalid Form")
    }
  }

  register() {
    this.processing  = true;
    this.authService.register(this.registerForm.value).then(
      data => {
        if (data) {
          alert("User account registered successfully.")
          this.router.navigate(['/login']);
        } else {
          this.handleRegisterError();
        }
      },
      err => {
        this.handleRegisterError();
      });
  }

  handleLoginSuccess() {
    this.processing = false;
    this.error  = false;
    this.router.navigate(['/dashboard']);
  }

}
