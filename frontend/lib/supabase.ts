import { createClient } from '@supabase/supabase-js';

export const supabase = createClient(
  'https://osscywdovhqwoqptapdx.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9zc2N5d2Rvdmhxd29xcHRhcGR4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA1MTUyNzYsImV4cCI6MjA3NjA5MTI3Nn0.oUjIuvHhEsykkL71_q3cXlm1Z7baltfIIzDREa-oJmE'
);