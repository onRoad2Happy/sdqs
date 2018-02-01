import { TestBed, inject } from '@angular/core/testing';

import { StreamDataService } from './stream-data.service';

describe('StreamDataService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [StreamDataService]
    });
  });

  it('should be created', inject([StreamDataService], (service: StreamDataService) => {
    expect(service).toBeTruthy();
  }));
});
