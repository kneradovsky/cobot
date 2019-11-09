import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';
import { CUser } from '../user';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss']
})
export class UserComponent implements  OnInit {
  users: Array<CUser>;
  currentUser: CUser;
  constructor(private srv: UserService) { }

  ngOnInit() {
    this.srv.list.subscribe((users) => this.users = users);
  }

  selectUser(i: number) {
    this.currentUser = this.users[i];
  }

  updateUser() {
    this.srv.update(this.currentUser);
  }

}
