import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { environment } from 'src/environments/environment';
import { AuthService } from '../_auth/services/auth.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  totalJobs: number = 0;
  totalResumes: number = 0;


  constructor(private http: HttpClient, private authService: AuthService) { }

  ngOnInit(): void {
    this.http.get(environment['apiBaseUrl'] + 'resumes/', {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${this.authService.getToken()}`,
        'Content-Type': 'application/json'
      })
    }).subscribe((response: any) => {
      if (response?.length) {
        this.totalResumes = response.length
      }
      // this.datas = response;
    }, err => {
      console.log(err)
    });

    this.http.get(environment['apiBaseUrl'] + 'jobs/', {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${this.authService.getToken()}`,
        'Content-Type': 'application/jsn'
      })
    }).subscribe((response: any) => {
      this.totalJobs = response.length ;
    }, err => {
      console.log(err)
    });

  }

}
