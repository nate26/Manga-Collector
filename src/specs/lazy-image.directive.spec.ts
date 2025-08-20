import { LazyImageDirective } from './lazy-image.directive';

describe('LazyImageDirective', () => {
  let nativeElementMock: jasmine.SpyObj<HTMLImageElement>;

  it('should add lazy attribute if it is supported', () => {
    nativeElementMock = jasmine.createSpyObj(['setAttribute']);
    const directive = new LazyImageDirective({ nativeElement: nativeElementMock });
    expect(directive).toBeTruthy();
    expect(nativeElementMock.setAttribute).toHaveBeenCalledWith('loading', 'lazy');
  });

  it('should not add lazy attribute if it is not supported', () => {
    const originalLoading = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, 'loading');

    nativeElementMock = jasmine.createSpyObj(['setAttribute']);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    delete (HTMLImageElement.prototype as any).loading;

    const directive = new LazyImageDirective({ nativeElement: nativeElementMock });
    expect(directive).toBeTruthy();
    expect(nativeElementMock.setAttribute).not.toHaveBeenCalled();

    Object.defineProperty(HTMLImageElement.prototype, 'loading', originalLoading!);
    expect('loading' in HTMLImageElement.prototype).toBe(true);
  });
});
