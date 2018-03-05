import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StreamAccuracyComponent } from './stream-accuracy.component';

describe('StreamAccuracyComponent', () => {
  let component: StreamAccuracyComponent;
  let fixture: ComponentFixture<StreamAccuracyComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StreamAccuracyComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StreamAccuracyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
