import { TestBed } from '@angular/core/testing';

import { MangaRecordService } from './manga-record.service';

describe('MangaRecordService', () => {
  let service: MangaRecordService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MangaRecordService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
