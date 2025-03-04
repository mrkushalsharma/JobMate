import { Component, OnInit } from '@angular/core';
import { AuthService } from '../_auth/services/auth.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'app-job',
  templateUrl: './job.component.html',
  styleUrls: ['./job.component.css']
})
export class JobComponent implements OnInit {

  datas: any = [];
  url = "";
  showModal: boolean = false;
  selected: any;

  constructor(private authService: AuthService,
    private spinner: NgxSpinnerService,
    private http: HttpClient
  ) {
  }

  ngOnInit(): void {
    console.log(this.url)
    this.http.get(environment['apiBaseUrl'] + 'jobs/getAll', {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${this.authService.getToken()}`,
        'Content-Type': 'application/jsn'
      })
    }).subscribe(response => {
      this.datas = response;
    }, err => {
      console.log(err)
    });
  }

  search() {
    this.spinner.show();
    this.http.post(environment['apiBaseUrl'] + 'jobs/add', {
      url: this.url
    }, {
      headers: new HttpHeaders({
        'accept': 'application/json',
        'Authorization': `Bearer ${this.authService.getToken()}`,
        'Content-Type': 'application/json'
      })
    }
    ).subscribe(response => {
      this.spinner.hide();
      alert("URL Successfully Crawled.")
      this.ngOnInit();
    }, err => {
      this.spinner.hide();
      alert("Error Occurred while Crawling URL")
      console.log(err);
    });
  }

  reset() {
    this.url = "";
  }

  apply(id: Number) {
    this.http.post(environment['apiBaseUrl'] + 'jobs/update_applied', `{\n  "id": ${id},\n  "applied": true\n}`, {
      headers: new HttpHeaders({
        'accept': 'application/json',
        'Authorization': `Bearer ${this.authService.getToken()}`,
        'Content-Type': 'application/json'
      })
    }
    ).subscribe(response => {
      alert("Successfully Applied")
      this.ngOnInit();
    }, err => {
      console.log(err)
    });
  }

  openModal(item: any) {
    // Simulate fetching data from API
    this.selected = item;
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

}
