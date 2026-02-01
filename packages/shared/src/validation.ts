// Input validation utilities
export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

export function validateFilePath(path: string): ValidationResult {
  const errors: string[] = [];
  
  if (!path || typeof path !== 'string') {
    errors.push('File path must be a non-empty string');
  } else {
    if (path.includes('..')) {
      errors.push('File path cannot contain ".." segments');
    }
    if (path.startsWith('/') && process.platform === 'win32') {
      errors.push('Absolute Unix paths not supported on Windows');
    }
    if (path.length > 260 && process.platform === 'win32') {
      errors.push('File path exceeds Windows maximum length');
    }
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}

export function validateSearchQuery(query: string): ValidationResult {
  const errors: string[] = [];
  
  if (!query || typeof query !== 'string') {
    errors.push('Search query must be a non-empty string');
  } else {
    if (query.trim().length === 0) {
      errors.push('Search query cannot be empty or whitespace only');
    }
    if (query.length > 1000) {
      errors.push('Search query too long (max 1000 characters)');
    }
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}

export function validatePort(port: number): ValidationResult {
  const errors: string[] = [];
  
  if (!Number.isInteger(port)) {
    errors.push('Port must be an integer');
  } else {
    if (port < 1 || port > 65535) {
      errors.push('Port must be between 1 and 65535');
    }
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}

export function validateServiceName(name: string): ValidationResult {
  const errors: string[] = [];
  
  if (!name || typeof name !== 'string') {
    errors.push('Service name must be a non-empty string');
  } else {
    if (!/^[a-z][a-z0-9-]*[a-z0-9]$/.test(name)) {
      errors.push('Service name must be lowercase, start with letter, and contain only letters, numbers, and hyphens');
    }
    if (name.length > 50) {
      errors.push('Service name too long (max 50 characters)');
    }
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}