import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventrequestComponent } from './eventrequest.component';

describe('EventrequestComponent', () => {
  let component: EventrequestComponent;
  let fixture: ComponentFixture<EventrequestComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EventrequestComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventrequestComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
