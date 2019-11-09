import { Injectable } from '@angular/core';
import { ConfigService } from './config.service';
import { Observable } from 'rxjs';
import { map} from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import {ELocation} from './location';


@Injectable({
  providedIn: 'root'
})
export class LocationsService {

  constructor(private cfg: ConfigService, private http: HttpClient) { }

  public get list() {
    return this.http.get<Array<ELocation>>(this.cfg.apiUrl + '/locations');
  }

  public delete(loc: ELocation): Observable<boolean> {
    return this.http.delete<{deleted: number}>(this.cfg.apiUrl + '/locations').pipe(
      map(res => {
        if (res.deleted > 0) {return true;}
        return false;
      })
    );
  }

}
