import { Injectable } from '@angular/core';
import { ConfigService } from './config.service';
import { HttpClient } from '@angular/common/http';
import { CEvent, CEventRequest } from './cevent';

@Injectable({
  providedIn: 'root'
})
export class EventsService {

  constructor(private cfg: ConfigService, private http: HttpClient) { }

  public get list() {
    return this.http.get<Array<CEvent>>(this.cfg.apiUrl + '/events');
  }

  public get list_requests() {
    return this.http.get<Array<CEventRequest>>(this.cfg.apiUrl + '/event_reqs');
  }
}
