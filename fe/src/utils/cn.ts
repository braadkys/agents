import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * Utility to merge tailwind classes with clsx syntax and library support
 */
export const cn = (...args: ClassValue[]) => {
  return twMerge(clsx(args))
}
