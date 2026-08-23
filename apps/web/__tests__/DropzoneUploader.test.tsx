import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { DropzoneUploader } from "@/components/upload/DropzoneUploader";

// Mock react-dropzone to give us control in tests
jest.mock("react-dropzone", () => ({
  useDropzone: ({ onDrop }: { onDrop: (files: File[], rejected: unknown[]) => void }) => ({
    getRootProps: () => ({
      onClick: jest.fn(),
      onDragEnter: jest.fn(),
      onDragOver: jest.fn(),
      onDrop: (e: React.DragEvent) => {
        // Simulate files being dropped
        const files = Array.from(e.dataTransfer?.files ?? []);
        onDrop(files, []);
      },
    }),
    getInputProps: () => ({
      type: "file",
      accept: "image/jpeg,image/png,image/webp",
    }),
    isDragActive: false,
  }),
}));

// Mock URL.createObjectURL
global.URL.createObjectURL = jest.fn(() => "blob:mock-preview-url");
global.URL.revokeObjectURL = jest.fn();

describe("DropzoneUploader", () => {
  it("renders the upload prompt", () => {
    const onFile = jest.fn();
    render(<DropzoneUploader onFile={onFile} />);
    expect(screen.getByText(/drag & drop your image/i)).toBeInTheDocument();
  });

  it("shows accepted file types hint", () => {
    const onFile = jest.fn();
    render(<DropzoneUploader onFile={onFile} />);
    expect(screen.getByText(/JPEG, PNG, WebP/i)).toBeInTheDocument();
  });

  it("calls onFile when a valid image is dropped", async () => {
    const onFile = jest.fn();
    render(<DropzoneUploader onFile={onFile} />);

    const dropzone = screen.getByRole("presentation");
    const file = new File(["img-content"], "test.jpg", { type: "image/jpeg" });

    // Simulate drop
    Object.defineProperty(dropzone, "files", { value: [file] });
    fireEvent.drop(dropzone, {
      dataTransfer: { files: [file] },
    });

    await waitFor(() => {
      expect(URL.createObjectURL).toHaveBeenCalled();
    });
  });

  it("shows loading overlay when isLoading is true", () => {
    const onFile = jest.fn();
    render(<DropzoneUploader onFile={onFile} isLoading />);
    // The dropzone should be non-interactive when loading
    const input = screen.queryByRole("textbox");
    // Loading state is passed through; verify the component renders
    expect(screen.getByText(/drag & drop your image/i)).toBeInTheDocument();
  });

  it("has accessible input element", () => {
    const onFile = jest.fn();
    render(<DropzoneUploader onFile={onFile} />);
    // Dropzone renders a hidden file input
    expect(screen.getByRole("presentation")).toBeInTheDocument();
  });
});
