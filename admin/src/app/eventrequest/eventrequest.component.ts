import { Component, OnInit } from '@angular/core';
import { EventsService } from '../events.service';
import {CEvent, CEventRequest} from '../cevent';

@Component({
  selector: 'app-eventrequest',
  templateUrl: './eventrequest.component.html',
  styleUrls: ['./eventrequest.component.scss']
})
export class EventrequestComponent implements OnInit {
  eventReqs: Array<CEventRequest>;
  constructor(private srv: EventsService) { }

  ngOnInit() {
    this.srv.list_requests.subscribe(data => this.eventReqs=data);
  }

}
