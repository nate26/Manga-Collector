import { TestBed } from '@angular/core/testing';
import { SearchService } from '../../../app/services/data/search.service';
import { Apollo } from 'apollo-angular';

describe('SearchService', () => {
    let service: SearchService;

    let apolloMock: jasmine.SpyObj<Apollo>;

    beforeEach(() => {
        apolloMock = jasmine.createSpyObj(['watchQuery']);
        TestBed.configureTestingModule({
            providers: [
                { provide: Apollo, useValue: apolloMock }
            ]
        });
        service = TestBed.inject(SearchService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
});
