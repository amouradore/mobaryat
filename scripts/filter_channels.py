import argparse

def filter_channels(input_file, output_file, include_keywords=None, exclude_keywords=None):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        line_iterator = iter(infile)
        for line in line_iterator:
            if line.startswith('#EXTINF'):
                # Read the URL line immediately after #EXTINF
                try:
                    url_line = next(line_iterator)
                except StopIteration:
                    # Reached end of file unexpectedly after #EXTINF
                    continue

                line_lower = line.lower()
                
                # Check for inclusion
                include = True
                if include_keywords:
                    include = any(keyword in line_lower for keyword in include_keywords)
                
                # Check for exclusion
                exclude = False
                if exclude_keywords:
                    exclude = any(keyword in line_lower for keyword in exclude_keywords)

                if include and not exclude:
                    outfile.write(line)
                    outfile.write(url_line)
            else:
                # Write non-#EXTINF lines as is if they are not URLs following a #EXTINF
                # This part is a bit tricky, M3U usually has EXTINF then URL. 
                # For simplicity, we assume only EXTINF and URL lines are relevant.
                pass # We will skip non #EXTINF and non-URL lines for now

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Filter M3U playlist channels based on keywords.")
    parser.add_argument('input_m3u_file', help="Path to the input M3U file.")
    parser.add_argument('output_m3u_file', help="Path to the output M3U file.")
    parser.add_argument('--include', nargs='*', help="Keywords to include (case-insensitive). Channels must contain at least one of these.")
    parser.add_argument('--exclude', nargs='*', help="Keywords to exclude (case-insensitive). Channels containing any of these will be excluded.")
    
    args = parser.parse_args()
    
    # Convert include and exclude keywords to a set for faster lookup and lowercasing them
    include_kws = [kw.lower() for kw in args.include] if args.include else None
    exclude_kws = [kw.lower() for kw in args.exclude] if args.exclude else None

    filter_channels(args.input_m3u_file, args.output_m3u_file, include_keywords=include_kws, exclude_keywords=exclude_kws)
