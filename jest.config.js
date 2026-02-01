/** @type {import('jest').Config} */
export default {
  preset: 'ts-jest/presets/default-esm',
  extensionsToTreatAsEsm: ['.ts'],
  moduleNameMapping: {
    '^(\\.{1,2}/.*)\\.js$': '$1',
    '^@nexus/(.*)$': '<rootDir>/packages/$1/src'
  },
  testEnvironment: 'node',
  testMatch: [
    '<rootDir>/packages/**/__tests__/**/*.test.ts',
    '<rootDir>/services/**/__tests__/**/*.test.ts'
  ],
  collectCoverageFrom: [
    'packages/**/src/**/*.ts',
    'services/**/src/**/*.ts',
    '!**/*.d.ts',
    '!**/node_modules/**'
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testTimeout: 10000,
  maxWorkers: '50%'
};