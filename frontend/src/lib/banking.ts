const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
    cache: "no-store",
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail ?? "The demo banking service could not complete the request.");
  }
  return data as T;
}

export type Account = {
  id: string;
  owner: string;
  type: string;
  balance: string;
  currency: string;
};

export type ApiTransaction = {
  id: string;
  account_id: string;
  description: string;
  amount: string;
  direction: "credit" | "debit";
  status: string;
  created_at: string;
};

export type TransferResult = {
  message: string;
  transaction: ApiTransaction;
  new_balance: string;
};

export function getAccounts() {
  return request<Account[]>("/api/accounts");
}

export function getTransactions() {
  return request<ApiTransaction[]>("/api/transactions");
}

export function createTransfer(payload: {
  from_account: string;
  beneficiary: string;
  amount: number;
  note: string;
}) {
  return request<TransferResult>("/api/transfers", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
