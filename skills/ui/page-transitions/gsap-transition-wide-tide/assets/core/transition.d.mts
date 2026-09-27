export interface Shape {
  id: string; name: string; description: string;
  start: readonly [number, number];
  curves: ReadonlyArray<readonly [number, number, number, number, number, number]>;
  initialStroke: number; coverStroke: number; drawnAtCover: number;
  scale: number; offset: number; thickenAt?: number;
}
export interface Session {
  signal: AbortSignal;
  covered: Promise<boolean>;
  current(): boolean;
  cancel(): void;
  reduce(): void;
  reveal(ready?: Promise<unknown>, timeoutMs?: number): Promise<boolean>;
}
export interface Transition {
  begin(signal?: AbortSignal): Session;
  cancel(): void;
  reduce(): void;
  destroy(): void;
  run<T>(options: {
    load(signal: AbortSignal): T | Promise<T>;
    swap(destination: T, signal: AbortSignal): void | Promise<void>;
    ready?(signal: AbortSignal): Promise<unknown>;
    signal?: AbortSignal; timeoutMs?: number;
  }): Promise<boolean>;
}
export function createTransition(options: {
  overlay: HTMLElement;
  gsap: { to(target: object, vars: Record<string, unknown>): { kill(): void } };
  variant?: string; shape?: Shape; color?: string; portraitMaxWidth?: number;
  portrait?: { initialStroke?: number; coverStroke?: number };
  lock?: () => () => void;
}): Transition;
export function visibleMediaReady(doc?: Document): Promise<unknown[]>;
export function getShape(name?: string): Shape;
export const SHAPES: Shape[];
export const VARIANTS: Array<{ name: string; id: string }>;
export const TIMING: Readonly<{ drawDuration: number; thickenAt: number; swapAt: number; revealDuration: number; duration: number; fps: number }>;
export function frame(time: number, shape: Shape): { incoming: boolean; start: number; end: number; stroke: number; visible: boolean };
export function portraitShape(source: Shape, width: number, height: number, options?: { initialStroke?: number; coverStroke?: number }): { viewportHeight: number; shape: Shape };
