import { Component, OnInit } from '@angular/core';

import { AuthService } from '../_auth/services/auth.service';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.css']
})
export class LogoutComponent implements OnInit {

  constructor(
    private authService: AuthService,
  ) { }

  ngOnInit() {
    this.authService.logout();
  }

}
