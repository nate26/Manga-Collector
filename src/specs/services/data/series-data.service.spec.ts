import { TestBed } from '@angular/core/testing';

import { SeriesDataService } from './series-data.service';

describe('SeriesDataService', () => {
  let service: SeriesDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SeriesDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
