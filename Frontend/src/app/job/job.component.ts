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

  showResumeModal: boolean = false; // Modal visibility
  selectedJobId: any; // Selected job ID for association
  selectedResumeId: any; // Selected resume ID for association
  resumes: any[] = []; // Array to hold resumes
  matchValue: any = {};
  
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
    this.getResumes();
  }

  getResumes(){
    this.http.get(environment['apiBaseUrl'] + 'resumes/', {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${this.authService.getToken()}`,
        'Content-Type': 'application/json'
      })
    }).subscribe((response: any) => {
      this.resumes = response;
    }, err => {
      console.log(err);
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
    this.selected = {};
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

    // New method to open the resume modal
    openResumeModal(job: any) {
      this.selectedJobId = job.id; // Set the selected job ID
      this.showResumeModal = true; // Show the resume modal
      this.matchValue = {};
    }
  
    // New method to close the resume modal
    closeResumeModal() {
      this.showResumeModal = false; // Hide the resume modal
      this.selectedResumeId = null; // Reset selected resume ID
    }
  
    // New method to match a resume with a job
    matchResume(jobId: number, resumeId: number) {
      // this.http.get(`${environment['apiBaseUrl']}matches/jobs/${jobId}/resumes/${resumeId}`, {
      //   headers: new HttpHeaders({
      //     'Authorization': `Bearer ${this.authService.getToken()}`,
      //     'Content-Type': 'application/json'
      //   })
      // }).subscribe(response => {
      //   // this.ngOnInit(); // Refresh the job list
      //   this.closeResumeModal(); // Close the modal after association
      //   alert("Resume Matched Successfully")
      // }, err => {
      //   console.log(err);
      // });
      if(!resumeId){
        return;
      }
      this.http.post(`${environment['apiBaseUrl']}matches/calculate-all/jobs/${jobId}`, {}, {
        headers: new HttpHeaders({
          'Authorization': `Bearer ${this.authService.getToken()}`,
          'Content-Type': 'application/json'
        })
      }).subscribe((response: any) => {
        const match = response.find((item: any) => item.resume_id == resumeId);
        if (match) {
          this.matchValue = match; // Set the match score
        } else {
          this.matchValue = {}; // Reset if no match found
        }
      }, err => {
        console.log(err);
      });
    }
  
}
