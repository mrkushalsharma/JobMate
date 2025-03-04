import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Subject, BehaviorSubject } from 'rxjs';
import { environment } from '../../../environments/environment';
import { UserModel } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  isLoggedIn = new BehaviorSubject(false);

  private token: any = "";
  private userData: UserModel | any = null;

  constructor(
    private http: HttpClient,
  ) {
    // try and find out if there was a localstorage token was set
    this.resolveToken();
  }

  // check if localstorage token was set
  // if so, set the token in the service
  // and set the login status
  resolveToken(): boolean {
    this.token = localStorage?.getItem('access_token');
    this.isLoggedIn.next(this.token ? true : false);
    return this.token ? true : false;
  }

  getToken(): string {
    return this.token;
  }

  hasToken(): boolean {
    return this.getToken() ? true : false;
  }

  async logout() {
    this.clearData();
    this.isLoggedIn.next(false);
    return true;
  }

  async login({ email, password }: UserModel): Promise<any> {
    // clear some data
    this.clearData();
    const formData = new FormData();
    formData.append('username', email || "");
    formData.append('password', password || "");

    const data: any = await this.http.post(environment['apiBaseUrl'] + 'login', formData).toPromise();
    if (data['access_token']) {
      let user = this.parseJwt(data['access_token']);
      data.user = user;
      this.setDataAfterLogin(data);
      this.isLoggedIn.next(true); // how do I unit test this?

      return user;
    } else {
      return false;
    }
  }

  async register({ email, password }: UserModel): Promise<any> {
    const data: any = await this.http.post(environment['apiBaseUrl'] + 'users/', {
      email: email,
      password: password
    }).toPromise();
    if (data && data.id) {
      return true;
    } else {
      return false;
    }
  }

  parseJwt(token: any) {
    try {
      return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
      return null;
    }
  }

  clearData() {
    this.userData = null;
    this.token = "";
    localStorage.clear();
  }

  getUserData() {
    return JSON.parse(localStorage.getItem('user') || "")
  }

  private setDataAfterLogin(data: any) {
    this.token = data['access_token'];

    // store some user data in the service
    this.userData = data['user'];

    // store some data in local storage (webbrowser)
    localStorage.setItem('access_token', this.token);
    localStorage.setItem('user', JSON.stringify(this.userData));
  }
}
