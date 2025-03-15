import 'react';
import { NextPage } from 'next';
import { AppProps } from 'next/app';
import { ReactElement, ReactNode } from 'react';

declare global {
  // NextJS specific types
  export type NextPageWithLayout<P = {}, IP = P> = NextPage<P, IP> & {
    getLayout?: (page: ReactElement) => ReactNode;
  };

  export type AppPropsWithLayout = AppProps & {
    Component: NextPageWithLayout;
  };

  // Custom types
  export interface AuthState {
    isAuthenticated: boolean;
    user: any | null;
    loading: boolean;
    error: string | null;
  }
} 