import { Component, OnInit } from '@angular/core';
import { EventsService } from '../events.service';
import {CEvent} from '../cevent';

@Component({
  selector: 'app-events',
  templateUrl: './events.component.html',
  styleUrls: ['./events.component.scss']
})
export class EventsComponent implements OnInit {

  events: Array<CEvent>;
  constructor(private srv: EventsService) { }

  ngOnInit() {
    this.srv.list.subscribe((data) => this.events = data);
  }

}
