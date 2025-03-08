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
  showModal: boolean = false;
  selected: any;
  showAddEditModal: boolean = false; // New property for add/edit modal visibility
  isEditMode: boolean = false; // New property to determine if in edit mode
  newJob: any = { title: '', company: '', description: '' }; // New property for new job data
  submitted: boolean = false;

  constructor(private authService: AuthService,
    private spinner: NgxSpinnerService,
    private http: HttpClient
  ) {
  }

  ngOnInit(): void {
    this.http.get(environment['apiBaseUrl'] + 'jobs/', {
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

  delete(id: number) {
    this.http.delete(`${environment['apiBaseUrl']}jobs/${id}`, { // Changed to include job ID in the URL
      headers: new HttpHeaders({
        'accept': '*/*', // Updated accept header to match curl
        'Authorization': `Bearer ${this.authService.getToken()}`,
        'Content-Type': 'application/json'
      })
    }).subscribe(response => {
      this.ngOnInit();
    }, err => {
      console.log(err);
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

  openAddModal() {
    this.isEditMode = false; // Set to add mode
    this.showAddEditModal = true; // Show the add job modal
    this.newJob = { title: '', company: '', description: '' }; // Reset new job data
  }

  openEditModal(item: any) {
    this.isEditMode = true; // Set to edit mode
    this.showAddEditModal = true; // Show the edit job modal
    this.newJob = { ...item }; // Populate the form with the selected job data
  }

  closeAddEditModal() {
    this.showAddEditModal = false; // Hide the add/edit job modal
    this.newJob = { title: '', company: '', description: '' }; // Reset new job data
  }

  createJob() {
    this.submitted = true; // Set submitted to true for validation
    if (this.newJob.title && this.newJob.company && this.newJob.description) {
      this.http.post(environment['apiBaseUrl'] + 'jobs/', this.newJob, {
        headers: new HttpHeaders({
          'Authorization': `Bearer ${this.authService.getToken()}`,
          'Content-Type': 'application/json'
        })
      }).subscribe(response => {
        this.ngOnInit(); // Refresh the job list
        this.closeAddEditModal(); // Close the modal after creation
        this.submitted = false;
      }, err => {
        console.log(err);
      });
    }
  }

  updateJob() {
    this.submitted = true; // Set submitted to true for validation
    if (this.newJob.title && this.newJob.company && this.newJob.description) {
      this.http.put(environment['apiBaseUrl'] + 'jobs/' + this.newJob.id, this.newJob, {
        headers: new HttpHeaders({
          'Authorization': `Bearer ${this.authService.getToken()}`,
          'Content-Type': 'application/json'
        })
      }).subscribe(response => {
        this.ngOnInit(); // Refresh the job list
        this.closeAddEditModal(); // Close the modal after updating
        this.submitted = false;
      }, err => {
        console.log(err);
      });
    }
  }

}
