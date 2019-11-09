import { Component, OnInit } from '@angular/core';
import { LocationsService } from '../locations.service';
import {ELocation} from '../location';


@Component({
  selector: 'app-locations',
  templateUrl: './locations.component.html',
  styleUrls: ['./locations.component.scss']
})
export class LocationsComponent implements OnInit {
  locations: Array<ELocation>;
  constructor(private locsrv: LocationsService) { }

  ngOnInit() {
    this.locsrv.list.subscribe((data: Array<ELocation>) => this.locations = data);
  }

}
