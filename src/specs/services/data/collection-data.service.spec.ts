import { TestBed } from '@angular/core/testing';
import { CollectionDataService } from '../../../app/services/data/collection-data.service';

describe('CollectionDataService', () => {
    let service: CollectionDataService;

    beforeEach(() => {
        TestBed.configureTestingModule({});
        service = TestBed.inject(CollectionDataService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
});
